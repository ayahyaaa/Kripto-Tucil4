from flask import Flask, render_template, request
import src as algo

app = Flask(__name__)

@app.route('/' , methods=["GET", "POST"])
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=["GET", "POST"])
def encrypt():
    if (request.method == "POST"):
        cypher = request.form['methodInput']
        message = request.form['messageinput'].lower().replace(" ","")
        if (cypher=="RSA"):
            p = int(request.form['pInput']) 
            q = int(request.form['qInput']) 
            e = int(request.form['eInput']) 
            (n,toitent) = algo.ersa1(p,q)
            encrypt = algo.ersa2(n,e,message)
            print(encrypt)
            return render_template("index.html", answer = encrypt, mode = "encrypted")
        elif (cypher=="ElGamal"):
            p = int(request.form['pInput']) 
            g = int(request.form['gInput']) 
            x = int(request.form['xInput']) 
            k = int(request.form['kInput']) 
            y = algo.elgamalkey(p,g,x)
            enc1, enc2 = algo.eelgamal(y,p,g,k,message)
            enc1.append(enc2)
            return render_template("index.html", answer = enc1, mode = "encrypted")
        elif (cypher=="Paillier"):
            p = int(request.form['pInput']) 
            q = int(request.form['qInput']) 
            g = int(request.form['gInput']) 
            r = int(request.form['rInput']) 
            n, yss, myu = algo.paillierkey(p,q,g)
            enc = algo.epaillier(p,g,n,r,message)
            return render_template("index.html", answer = enc, mode = "encrypted")
    else:
        return render_template("index.html")

@app.route('/decrypt', methods=["GET", "POST"])
def decrypt():
    if (request.method == "POST"):
        cypher = request.form['methodInput']
        encrypted = request.form['cypher1Input']
        if (cypher=="RSA"):
            print("rsa")
            p = int(request.form['pInput'])
            q = int(request.form['qInput'])
            (n,toitent) = algo.ersa1(p,q)
            e = int(request.form['eInput']) 
            decrypt = algo.drsa(n,toitent,e,encrypted)
            return render_template("index.html", answer1 = decrypt, mode= "decrypted")
        elif (cypher=="ElGamal"):
            p = int(request.form['pInput']) 
            x = int(request.form['xInput']) 
            encrypted2 = request.form['cypher2Input']
            enc1 = encrypted.split(", ")
            enc2 = encrypted2.split(", ")
            for i in range(len(enc1)):
                enc1[i] = int(enc1[i])
            for i in range(len(enc2)):
                enc2[i] = int(enc2[i])
            decrypted = algo.delgamal(x,p,enc1,enc2)
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
        elif (cypher=="Paillier"):
            p = int(request.form['pInput']) 
            q = int(request.form['qInput']) 
            g = int(request.form['gInput']) 
            n, yss, myu = algo.paillierkey(p,q,g)
            encrypt = encrypted.split(", ")
            for i in range(len(encrypt)):
                encrypt[i] = int(encrypt[i])
            decrypted = algo.dpaillier(p,n,yss,myu,encrypt)
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
    else:
        return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)