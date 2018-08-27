$(document).ready(function(){
            $('[data-toggle="popover"]').popover();
        });

            function myFunction() {
                var x = document.getElementById("myDIV");
                var y = document.getElementById("myDIV1");
                y.style.display = "none"

                if (x.style.display === "none") {
                    x.style.display = "block";
                } else {
                   none;
                }
            }

            function myFunction1() {
                var x = document.getElementById("myDIV1");
                var y = document.getElementById("myDIV");
                y.style.display = "none"
                if (x.style.display === "none") {
                    x.style.display = "block";
                } else {
                    none;
                }
            }

             function AvoidSpace(event) {
    var k = event ? event.which : window.event.keyCode;
    if (k == 32) return false;
}



