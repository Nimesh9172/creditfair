if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

$(document).ready(()=>{
        
////////////////////////////sidebar functions///////////////////
 
    $(".sidebar").mouseover(function(){
        $(".sidebar").removeClass("close")
    })
    $(".sidebar").mouseout(function(){
        $(".sidebar").addClass("close")
    }); 

    $('.arrow2').click(function(){
        $(this).toggleClass('showMenu')
    })

    $('.iocn-link').parent().mouseleave(function(){
        $(this).removeClass('showMenu')
    })
////////////////////////////sidebar functions/////////////////// 
///////////////////select2 jquery start//////////////////////////
$('#rm-sortby').select2({
    minimumResultsForSearch: -1
});
$('.np-select').select2({
    minimumResultsForSearch: -1
});
///////////////////select2 jquery end//////////////////////////

})

