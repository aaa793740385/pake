window.onload = function time() {
        //�����ʾʱ���div
        t_span = document.getElementById('time');
        t_span.innerHTML = new Date().toString();
        //�ȴ�һ���Ӻ����time����������settimeout��time�����ڣ����Կ������޵���
        setTimeout(time, 1000);
    }