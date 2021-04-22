/*FUNCION MUSICA*/
function musicaP() {
    var ado1 = document.getElementById("sonido1");
    ado1.pause();
    var ado2 = document.getElementById("sonido2");
    ado2.pause();
    var ado3 = document.getElementById("sonido3");
    ado3.pause();
    var ado4 = document.getElementById("sonido4");
    ado4.pause();
    var ado5 = document.getElementById("sonido5");
    ado5.pause();
    var ado6 = document.getElementById("sonido6");
    ado6.pause();
}

function musicaF() {
    var ado = document.getElementById("musica");
    ado.volume = 0.15;
    ado.play();
}

function musicaS(x) {
    musicaP();
    var ado1 = document.getElementById("sonido1");
    var ado2 = document.getElementById("sonido2");
    var ado3 = document.getElementById("sonido3");
    var ado4 = document.getElementById("sonido4");
    var ado5 = document.getElementById("sonido5");
    var ado6 = document.getElementById("sonido6");
    
    if (x == 1){
        ado1.volume = 0.2;
        ado1.play();
    } else if(x == 2){
        ado2.volume = 0.1;
        ado2.play();
    } else if(x == 3){
        ado3.volume = 0.1;
        ado3.play();
    } else if(x == 4){
        ado4.volume = 0.15;
        ado4.play();
    } else if(x == 5){
        ado5.volume = 0.15;
        ado5.play();
    } else{
        ado6.volume = 0.15;
        ado6.play();
    }
}
