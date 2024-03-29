$(document).ready(function() {
    const canvas = $("#canvas").get(0);
    const canvas_parent = $("#canvas").parent();

    const ctx = canvas.getContext('2d');
    let prevX = null;
    let prevY = null;
    let draw = false;

    $(window).on("resize rightnow", function(){
        canvas.height = canvas_parent.innerHeight();
        canvas.width = canvas_parent.innerWidth();
    }).triggerHandler("rightnow");

    $(".clr").on("click", function (ev) {
        ev.preventDefault();
        let btn = ev.target;
        ctx.strokeStyle = btn.dataset.clr;
    });

    $("#clearBtn").on("click", function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    $("#addImageBtn").on("click", function () {
        const content = tinymce.activeEditor.getContent();
        tinymce.activeEditor.setContent(content + '<br><img alt="Image" style="display: block; margin-left: auto; margin-right: auto;" height="250" width="250" src="' + canvas.toDataURL("imag/png") + '"/><br>');
    });

    $("#penSize").on("input rightnow", function () {
        const value = $(this).val();
        $("#penSizeText").val(value);
        ctx.lineWidth = value;
    }).triggerHandler("rightnow");

    canvas_parent.on("mousedown", (e) => draw = true);
    canvas_parent.on("mouseup", (e) => draw = false);

    canvas_parent.on("mousemove", (e) => {
        if(prevX == null || prevY == null || !draw){
            prevX = e.clientX;
            prevY = e.clientY - 56.5;
            return;
        }
        let currentX = e.clientX;
        let currentY = e.clientY - 56.5;

        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currentX, currentY);
        ctx.stroke();

        prevX = currentX;
        prevY = currentY;
    })
});
