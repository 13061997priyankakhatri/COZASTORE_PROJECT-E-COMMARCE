from django.shortcuts import render,redirect
from .models import *
import random
import requests
from django.conf import settings
import razorpay
# Create your views here.

def index(request):
    product = Product.objects.all()
    return render(request,"index.html",{'product':product})

def sindex(request):
    return render(request,"sindex.html")

def product(request,cat):
    try :
        product=Product()
        if cat=='all':
            product = Product.objects.all()
        elif cat=='women':
            product = Product.objects.filter(pcategory='Women')
        elif cat=='men':
            product = Product.objects.filter(pcategory='Men')
        elif cat=='child':
            product = Product.objects.filter(pcategory='Child')
        return render(request,"product.html",{'product': product})
    except:
        return redirect("product") 

def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def signup(request):
    try:
        if request.method=="POST":
            try:
                User.objects.get(email=request.POST['email'])
                msg1 = "Email is Already register"
                return render(request,"signup.html",{'msg1':msg1})
            
            except:
                    if request.POST['password']==request.POST['cpassword']:
                        User.objects.create(
                            email = request.POST['email'],
                            firstname = request.POST['firstname'],
                            lastname = request.POST['lastname'],
                            mobile = request.POST['mobile'],
                            password = request.POST['password'],
                            role = request.POST['role'],
                            picture = request.FILES['picture']
                        )
                        msg = "Signup Successfully"
                        return render(request,'login.html',{'msg':msg})
                    else:
                        msg1 = "Password & confirm password does not match"
                        return render(request,"signup.html",{'msg1':msg1})

        else:
            return render(request,"signup.html")
    except:
        return redirect("signup")
        
def login(request):
    try:
        if request.method=="POST":
            try:
                user = User.objects.get(email=request.POST['email'])
                if user.password == request.POST["password"]:
                    request.session['email']=user.email
                    request.session['firstname']=user.firstname
                    request.session['picture']=user.picture.url
                    wishlist = Wishlist.objects.filter(user=user)
                    request.session['wishlist']=len(wishlist)
                    cart = Cart.objects.filter(user=user,payment=False)
                    request.session['cart']=len(cart)

                    if user.role == "buyer" :
                        return render(request,"index.html")
                    else :
                        return render(request,"sindex.html")
                else:
                    msg1 = "email and Password doesn't match"
                    return render(request,"login.html",{'msg1':msg1})
                
            except:
                msg1 = "email does not registered"
                return render(request,"signup.html")
        else :
            return render(request,"login.html")
    except:
        return redirect("login")

def logout(request):
    try :
        del request.session['email']
        del request.session['firstname']
        del request.session['picture']
        del request.session['wishlist']
        del request.session['cart']
        return redirect("login")
    except:
        return redirect("login")

def fpass(request):
    try :
        if request.method=="POST":  
            try: 
                User.objects.get(mobile=request.session['mobile'])
                mobile = request.POST['mobile']
                otp = random.randint(1001,9999)
                url = "https://www.fast2sms.com/dev/bulkV2"
                querystring = {"authorization":"tfUafDOabQAXAlemu5vWVAvKtmNvL4JXn57FnWVY0ehGefXQxO8i5AAc5PQL","variables_values":str(otp),"route":"otp","numbers":mobile}
                headers = {
                    'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                request.session['mobile']=mobile
                request.session['otp']=otp 
                print(mobile)
                print(otp)
                return render(request,"otp.html")
            except:
                return render(request,"fpass.html")    
        else:           
            return render(request,"fpass.html")
    except:
        return redirect("fpass")
        
def otp(request):
    try:
        if request.method=="POST":
            otp = int(request.session['otp'])
            uotp = int(request.POST['uotp'])
            print(type(otp))
            print(type(uotp))

            if otp==uotp:
                print("Hello")
                del request.session['otp']
                return render(request,"newpass.html")
            else:
                print("Hello")
                msg1 = "Invalid Otp"
                return render(request,"otp.html",{'msg1':msg1})
        else:    
            return render(request,"otp.html")
    except:
        return redirect("otp")
    
def newpass(request):
    try :
        if request.method =="POST":
            print("Hello")
            user = User.objects.get(mobile=request.session['mobile'])
            print("Hello")
            if request.POST['newpassword'] == request.POST['cnewpassword']:
                print("Hello")
                user.password = request.POST['newpassword']
                user.save()
                return render(request,"login.html")
            else:
                msg1 = "New password nad Confirm new password does not match"
                return render(request,"newpass.html",{'msg1':msg1,'user':user})            
        else:
            return render(request,"newpass.html")
    except:
        return redirect("newpass")

def cpass(request):
    try:
        user = User.objects.get(email=request.session['email'])
        if request.method=="POST":
            if user.password==request.POST['oldpassword']:
                if request.POST['newpassword']==request.POST['cnewpassword']:
                    user.password = request.POST['newpassword']
                    user.save()
                    return render(request,'login.html')
                else:
                    msg1 = "New password and Confirm new password doesn't match"
                    if user.role == "buyer" :
                        return render(request,'cpass.html',{'msg1':msg1})
                    else:
                        return render(request,"scpassword.html",{'msg1':msg1})
            else:
                msg1 = "Old password does not match"
                if user.role == "buyer" :
                    return render(request,'cpass.html',{'msg1':msg1})
                else:
                    return render(request,"scpassword.html",{'msg1':msg1})
        else:
            if user.role == "buyer" :
                return render(request,'cpass.html')
            else:
                return render(request,"scpassword.html")
    except:
        return redirect("cpass")
    
def profile(request):
    try:
        user = User.objects.get(email=request.session['email'])
        return render(request,"profile.html",{'user':user})
    except:
        return redirect("profile")

def add(request):
    try:
        seller=User.objects.get(email=request.session['email'])
        if request.method=="POST":
            Product.objects.create(
                seller=seller,
                pcategory=request.POST['pcategory'],
                psize=request.POST['psize'],
                pbrand=request.POST['pbrand'],
                pname=request.POST['pname'],
                desc=request.POST['desc'],
                price=request.POST['price'],
                ppicture=request.FILES['ppicture']               
            )
            msg = "Product Added Suceesfully!!"
            return render(request,"add.html",{'msg':msg})
        else:    
            return render(request,'add.html')
    except:
        return redirect("add")

def view(request):
    try:
        seller=User.objects.get(email = request.session['email'])
        product=Product.objects.filter(seller=seller)
        return render(request,'view.html',{'product':product})
    except:
        return redirect("view")

def pdetail(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        return render(request,"pdetail.html",{'product':product})
    except:
        return redirect("pdetail")

def pedit(request,pk):
    try :
        product = Product.objects.get(pk=pk)
        if request.method == "POST":
            product.pcategory = request.POST['pcategory']
            product.price = request.POST['price']
            product.pname = request.POST['pname']
            product.pbrand = request.POST['pbrand']
            product.psize = request.POST['psize']
            product.desc = request.POST['desc']
            try:
                product.ppicture = request.FILES['ppicture']
            except:
                pass
            product.save()
            msg = "Product Updated Sucessfully"
            return render(request,"pedit.html",{'product':product, 'msg':msg})
        else:
            return render(request,"pedit.html",{'product':product})
    except:
        return redirect("pedit")

def pdelete(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        product.save()
        return redirect("login")
    except:
        return redirect("login")

def bpdetail(request,pk):
    try :
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)
        wish = False
        cart = False
        try:
            Wishlist.objects.get(user=user,product=product)
            wish = True

        except:
            pass

        try:
            Cart.objects.get(user=user,product=product,payment=False)
            cart = True

        except:
            pass

        return render(request,"bpdetail.html",{'product':product,'wish':wish,'cart':cart})
    
    except:
        return redirect("bpdetail")

def addtowishlist(request,pk):
    try :
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)

        Wishlist.objects.create(user=user,product=product)
        return redirect("wishlist")
    except:
        return redirect("wishlist")

def wishlist(request):
    try:
        user = User.objects.get(email=request.session['email'])
        wishlist = Wishlist.objects.filter(user=user)
        request.session['wishlist']=len(wishlist)
        return render(request,"wishlist.html",{'wishlist':wishlist})
    except:
        return redirect("wishlist")

def deletetowishlist(request,pk):
    try:
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)

        wishlist = Wishlist.objects.get(user=user,product=product)
        wishlist.delete()
        return redirect("wishlist")
    except:
        return redirect("wishlist")

def addtocart(request,pk):
    try :
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)

        Cart.objects.create(user=user,
                            product = product,
                            tprice = product.price,
                            cqty = 1,
                            cprice = product.price,
                            payment = False
                            )
        return render(request,"addtocart.html")
    except:
        return render(request,"addtocart.html")

def shopping_cart(request):
    try :
        net = 0
        user = User.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(user=user,payment=False)
        request.session['cart']=len(cart)

        for i in cart :
            net += i.tprice
        
        if net>=20000 :
            ship = 0
        else :
            ship = 100

        sc = int(net+ship)
        print("****************",type(sc))
        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': sc * 100, 'currency': 'INR', 'payment_capture': 1})
        
        context =  {
                    'payment': payment
                }
        return render(request,"shopping_cart.html",{'cart':cart,'context':context,'sc':sc,'net':net,'ship':ship})
    except:
        return redirect("shopping_cart")

def deletetocart(request,pk):
    try:
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)

        cart = Cart.objects.get(user=user,product=product,payment=False)
        cart.delete()
        return redirect("shopping_cart")
    except:
        return redirect("shopping_cart")

def changequantity(request,pk):
    try:
        cart = Cart.objects.get(pk=pk,payment=False)
        cart.cqty = int(request.POST['cqty'])
        cart.save()
        cart.tprice = cart.cprice * cart.cqty
        cart.save()

        return redirect("shopping_cart")
    except:
        return redirect("shopping_cart")

def ajax(request):
    try:
     if request.POST:
        Ajax.objects.create(
            email=request.POST['email'],
            fname=request.POST['fname'],
            mobile=request.POST['mobile'],
        )
        msg = "Signup Succesfully"
        return render(request,"login.html",{'msg':msg})

     else:
         return render(request,"ajax.html")
    except:
        return redirect("ajax")
     
def success(request):
    try:
        user = User.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(user=user,payment=True)

        for i in cart:
            i.payment=True
            i.save()
        return render(request,"success.html",{'cart':cart})
    except:
        return redirect("success")

def myorder(request):
    try:
        user = User.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(user=user,payment=True)

        return render(request,"myorder.html",{'cart':cart})
    except:
        return redirect("myorder")

def jssignup(request):
    return render(request,"jssignup.html")