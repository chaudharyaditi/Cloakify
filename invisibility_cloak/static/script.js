document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const video = document.createElement('video');
    video.autoplay = true;
    video.playsInline = true;

    let cloakColor = 'red';
    let backgroundFrame = null;

    const form = document.getElementById('colorForm');
    form.addEventListener('submit', e => {
        e.preventDefault();
        const color = document.getElementById('color').value;
        fetch('/set_color', {
            method: 'POST',
            body: new URLSearchParams({ color })
        });
        cloakColor = color;
    });

    // Access webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;

            function captureBackground() {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                backgroundFrame = ctx.getImageData(0,0,canvas.width,canvas.height);
                console.log("[INFO] Background captured!");
            }

            // Capture background after 3 seconds
            setTimeout(captureBackground, 3000);

            function rgbToHsv(r,g,b){
                r/=255; g/=255; b/=255;
                let max=Math.max(r,g,b), min=Math.min(r,g,b);
                let h,s,v=max;
                let d=max-min;
                s=max===0?0:d/max;
                if(max===min){h=0;} 
                else {
                    switch(max){
                        case r: h=((g-b)/d+(g<b?6:0)); break;
                        case g: h=((b-r)/d+2); break;
                        case b: h=((r-g)/d+4); break;
                    }
                    h/=6;
                }
                return [h*360, s*100, v*100];
            }

            function draw() {
                if(!backgroundFrame){ requestAnimationFrame(draw); return; }

                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                let frame = ctx.getImageData(0,0,canvas.width,canvas.height);
                let data = frame.data;

                for(let i=0;i<data.length;i+=4){
                    let r=data[i], g=data[i+1], b=data[i+2];
                    let [h,s,v] = rgbToHsv(r,g,b);

                    let mask=false;
                    if(cloakColor==='red') mask = (h<10 || h>350) && s>50 && v>20;
                    if(cloakColor==='blue') mask = h>180 && h<250 && s>50 && v>20;
                    if(cloakColor==='green') mask = h>80 && h<160 && s>50 && v>20;

                    if(mask){
                        // Soft blending
                        let alpha = 0.7; 
                        data[i] = alpha*backgroundFrame.data[i] + (1-alpha)*r;
                        data[i+1] = alpha*backgroundFrame.data[i+1] + (1-alpha)*g;
                        data[i+2] = alpha*backgroundFrame.data[i+2] + (1-alpha)*b;
                    }
                }

                ctx.putImageData(frame,0,0);
                requestAnimationFrame(draw);
            }
            draw();
        })
        .catch(err => console.error("Camera error:", err));
});
