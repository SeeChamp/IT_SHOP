import os
import psycopg2
from model  import ProductCreate, UserCreate, Userlogin
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordBearer



app = FastAPI()


SECRET_KEY = "rabbit1158"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return int(user_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Token ไม่ถูกต้อง")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       
        return {"user_id":int(payload.get("sub")), 
                "role": payload.get("role")}

    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)



def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="ต้องเป็นแอดมินเท่านั้น")
    return current_user




conn = psycopg2.connect(    
    os.getenv("postgresql://postgres:dpJoNRKebPuUXgaeWKsyTthuxmfGHTrw@postgres.railway.internal:5432/railway")
)





@app.get("/products")
def get_products(current_user: dict = Depends(get_current_user)):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.id,
            p.name,
            p.price,
            u.username,
            c.name as category
        FROM products p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.user_id = %s
    """, (current_user["user_id"],))

    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "username": row[3],
            "category": row[4]
        })
    return results




@app.get("/admin")
def admin_only(user = Depends(require_admin)):
    return {"message": "ยินดีต้อนรับแอดมิน!"}

    



    
@app.post("/products")
def create_product(product: ProductCreate, current_user: dict = Depends(get_current_user)):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, condition, user_id, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (product.name, 
          product.description,
          product.price,
          product.condition,
          current_user["user_id"],
          product.category_id
    ))
    

    new_product_id = cursor.fetchone()[0]
    conn.commit()

    return {"id": new_product_id, "message": "สร้างข้อมูลสินค้าเรียบร้อยแล้ว"}





@app.post("/register")
def register(user: UserCreate):
    cursor = conn.cursor()
    hashed_password = hash_password(user.password)

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user.username, user.email, hashed_password, "user"))

        new_user_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "id": new_user_id,
            "message": "สมัครสมาชิกเรียบร้อยแล้ว"
        }

    except Exception as e:
        conn.rollback() 
        print("ERROR:", e)

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    



@app.post("/login")
def login(user: Userlogin):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, password_hash , role
        FROM users
        WHERE username = %s
    """, (user.username,))

    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=400, detail="ไม่พบผู้ใช้ในระบบ")
    
    user_id, hashed_password, role = result
    if not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=400, detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    
    access_token = create_access_token(data={"sub": str(user_id), "role": role})
    refresh_token = create_refresh_token(data={"sub": str(user_id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}





@app.post("/refresh")
def refresh_token(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")

    new_access_token = create_access_token(data={"sub": str(user_id)})

    return {"access_token": new_access_token, "token_type": "bearer"}






@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate, user_id: int = Depends(get_current_user)):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET name = %s,
            description = %s,
            price = %s,
            condition = %s,
            category_id = %s
        WHERE id = %s AND user_id = %s
        RETURNING id
    """, (product.name, 
          product.description,
          product.price,
          product.condition,
          product.category_id,
          product_id,
          user_id
    ))


    updated = cursor.fetchone()
    if not updated:
        raise HTTPException(status_code=403, detail="ไม่มีสิทธิ์แก้ไข")

    conn.commit()
    return {"message": "อัพเดตข้อมูลสินค้าเรียบร้อยแล้ว"}






@app.delete("/products/{product_id}")
def delete_product(product_id: int, current_user: dict = Depends(get_current_user)):
    cursor = conn.cursor()

    if current_user["role"] == "admin":
        cursor.execute("""
            DELETE FROM products
            WHERE id = %s
            RETURNING id
        """, (product_id,))
    else:

        cursor.execute("""
            DELETE FROM products
            WHERE id = %s AND user_id = %s
            RETURNING id
        """, (product_id, current_user["user_id"]))

    deleted = cursor.fetchone()

    if not deleted:
        raise HTTPException(status_code=403, detail="ไม่มีสิทธิ์ลบ")

    conn.commit()
    return {"message": "ลบข้อมูลสินค้าเรียบร้อยแล้ว"}


   