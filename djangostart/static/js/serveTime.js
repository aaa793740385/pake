window.onload = function time() {
        //获得显示时间的div
        t_span = document.getElementById('time');
        t_span.innerHTML = new Date().toString();
        //等待一秒钟后调用time方法，由于settimeout在time方法内，所以可以无限调用
        setTimeout(time, 1000);
    }