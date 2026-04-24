from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ดู working directory (optional)
print("cwd:", os.getcwd())

# 1. โหลดข้อมูล
df = pd.read_excel('Online Retail.xlsx', engine='openpyxl')

# 2. คำนวณยอดรวมต่อบิล (TotalPrice)  
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# 3. ทำ Data Cleaning  
#    – ลบรายการที่ไม่มี CustomerID  
#    – ลบ Quantity หรือ UnitPrice ที่ไม่เป็นบวก  
df = df.dropna(subset=['CustomerID'])
df = df[(df.Quantity > 0) & (df.UnitPrice > 0)]

# 4. สร้าง RFM Table  
#  4.1 กำหนด snapshot date (= วันหลังสุดใน dataset + 1 วัน)  
snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)

#  4.2 รวบรวม Recency, Frequency, Monetary  
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo':   'nunique',
    'TotalPrice':  'sum'
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# 5. ดูตาราง RFM ว่าถูกต้องไหม  
print(rfm.head())
print(rfm.describe().round(1))


#เตรียมข้อมูลก่อน Clustering
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

#หาจำนวน Cluster (Elbow Method & Silhouette)
inertia = []
sil_scores = []
K = range(2,10)
for k in K:
    km = KMeans(n_clusters=k, random_state=42).fit(rfm_scaled)
    inertia.append(km.inertia_)
    sil_scores.append(silhouette_score(rfm_scaled, km.labels_))

# Elbow
plt.plot(K, inertia, 'o-'); plt.title('Elbow'); plt.xlabel('k'); plt.ylabel('Inertia')
# Silhouette
plt.figure()
plt.plot(K, sil_scores, 'o-'); plt.title('Silhouette'); plt.xlabel('k'); plt.ylabel('Score')
plt.show()

plt.plot(K, inertia, 'o-')
plt.title('Elbow')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.savefig('elbow.png')  # บันทึกเป็นไฟล์
# plt.show()  <-- ถ้ายังมี ก็จะไม่พยายามเปิดหน้าต่าง


# …[รัน loop เก็บค่า inertia]…
plt.plot(K, inertia, 'o-')
plt.title('Elbow')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.show()


#สร้างโมเดล K-Means
best_k = 4  # สมมติได้จากข้อก่อนหน้า
km = KMeans(n_clusters=best_k, random_state=42)
rfm['Cluster'] = km.fit_predict(rfm_scaled)

#วิเคราะห์ผลลัพธ์ (Interpretation)
rfm.groupby('Cluster').mean().round(1)



pca = PCA(2)
coords = pca.fit_transform(rfm_scaled)
plt.figure(figsize=(6,5))
sns.scatterplot(x=coords[:,0], y=coords[:,1], hue=rfm.Cluster, palette='tab10')
plt.title('Customer Segments (PCA)')
plt.show()





print(rfm.dtypes)
# แสดงชนิดข้อมูลทุกคอลัมน์
print(df.dtypes)
# ใช้เมธอด info() แสดงทั้งชนิดข้อมูลและจำนวน non-null
df.info()
