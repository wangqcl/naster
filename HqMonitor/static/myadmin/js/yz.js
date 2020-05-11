/*验证密码*/
function checkPwd(password) {
    /*获取提示框*/
    var passwordMSG = document.getElementById("passwordMSG");
    /*定义正则表达式*/
    var reg = /^[a-zA-Z]\w{5,19}$/;
    var flag = reg.test(password);
    if ( !flag ) {
        passwordMSG.innerHTML = "<font color='red'>密码格式有误！</font>";
        Flag4 = false;
    } else {
        passwordMSG.innerHTML = "<font color='green'><b>√</b></font>";
        Flag4 = true;
    }
}

/*验证重复密码*/
var timeoutID;
function checkPwd2(pwd2) {
    /*获取提示框*/
    var mm2MSG = document.getElementById("mm2MSG");
    /*获取第一个框输入的密码*/
    var pwd1 = document.getElementById("password").value;
    //对上次未完成的延时操作进行取消
    clearTimeout(timeoutID);
    //对于密码比对延迟500ms，避免频繁比对
    timeoutID = setTimeout(function(){
        /*进行比对*/
        if(pwd1 != pwd2){
            Flag5 = false;
            mm2MSG.innerHTML = "<font color='red'>两次输入的密码不一致！</font>";
        } else {
            Flag5 = true;
            mm2MSG.innerHTML = "<font color='green'><b>√</b></font>";
        }
    },500);
}