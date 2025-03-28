# Encryption-Decryption-Tool
This tool provides a way to encrypt and decrypt files using Stored Key Method and Password-Based Key Derivation
## 🚀 Installation  

1. **Install Required Library**  
   ```bash
   pip install cryptography
   ```

---

## 🔹 Example Usage  

### **1. Generate a Key (Stored Key Method)**  
```bash
python script.py -g
```

---

### **2. Encrypt a File**  
- **Using Stored Key:**  
  ```bash
  python script.py -e -k myfile.txt
  ```
- **Using Password:**  
  ```bash
  python script.py -e -p myfile.txt
  ```

---

### **3. Decrypt a File**  
- **Using Stored Key:**  
  ```bash
  python script.py -d -k myfile.txt.encrypted
  ```
- **Using Password:**  
  ```bash
  python script.py -d -p myfile.txt.encrypted
  ```

---

✅ **Now you're all set!** 🚀
