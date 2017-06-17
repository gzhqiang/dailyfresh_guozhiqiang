#coding=utf-8
from django.shortcuts import render,redirect

from df_user import user_decorator
from df_user.models import UserInfo
from hashlib import sha1

#显示注册页面的视图
def register(request):
    return render(request,'df_user/register.html')


#处理用户注册请求
def register_handler(request):
    #接收请求参数
    user_name = request.POST['user_name']
    pwd = request.POST['pwd']
    cpwd = request.POST['cpwd']
    email = request.POST['email']
    if pwd != cpwd:
        return redirect('/user.register')

    #密码加密
    s1 = sha1()
    s1.update(pwd)
    upw3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = user_name
    user.upwd = upw3
    user.uemail = email
    user.save()
    #转到登陆页面
    return redirect('/user/login')


def login(request):
    uname = request.COOKIES.get('unme','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',uname)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post['username']
    upwd = post['pwd']
    jizhu = post.get('jizhu',0)

    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname = uname)

    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('red_url','/user/site')
            red = redirect(url)
            red.set_cookie('red_url','',max_age=-1)
            #记住用户名
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)




def logout(request):
    request.session.flush()
    return redirect('/user/site')


@user_decorator.login
def info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    goods_list = []
    goods_ids = request.COOKIES.get('liulan', '')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {
        'title': '用户中心',
        'user_email': user.uemail,
        'user_uphone': user.uphone,
        'user_uaddress': user.uaddress,
        'user_name': request.session['user_name'],
        'page_name': 1,
        'goods_list': goods_list,
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {
        'title': '用户中心',
        'user': user,
        'page_name': 1,
    }
    return render(request,'df_user/user_center_site.html',context)

