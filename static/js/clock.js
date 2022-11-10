const newTime = document.getElementById('time');
    
    function watch() {
        const Time = new Date(); 
        const year = Time.getFullYear(); 
        const hours = Time.getHours(); 
        const minutes = Time.getMinutes(); 
        const seconds = Time.getSeconds(); 

        newTime.innerHTML = zero(hours) + ':' + zero(minutes) + ':' + zero(seconds);
    }

    function zero(num) {
        if(num < 10) {
            num = '0' + num;
        }
        return num;
    }

    function init() {
        watch();
        setInterval(watch, 1000);
    }

    init();