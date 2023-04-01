if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}


// toast notification function start
error_icon = ` <svg style="margin-right:10px";  xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M6.99992 13.6666C3.31792 13.6666 0.333252 10.682 0.333252 6.99998C0.333252 3.31798 3.31792 0.333313 6.99992 0.333313C10.6819 0.333313 13.6666 3.31798 13.6666 6.99998C13.6666 10.682 10.6819 13.6666 6.99992 13.6666ZM6.33325 8.99998V10.3333H7.66659V8.99998H6.33325ZM6.33325 3.66665V7.66665H7.66659V3.66665H6.33325Z" fill="#C83532"></path>
</svg>`
success_icon = ` <svg style="margin-right:10px";  xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none">
      <path d="M6.99992 13.6667C3.31792 13.6667 0.333252 10.682 0.333252 7.00001C0.333252 3.31801 3.31792 0.333344 6.99992 0.333344C10.6819 0.333344 13.6666 3.31801 13.6666 7.00001C13.6666 10.682 10.6819 13.6667 6.99992 13.6667ZM6.22925 9.99001L10.9426 5.27601L9.99992 4.33334L6.22925 8.10468L4.34325 6.21868L3.40058 7.16134L6.22925 9.99001Z" fill="#2BAC47"/>
      </svg> `
function showToast(message,type) { 
    // Create a new toast element
    console.log("asdassd")
    type == 1 ?  document.getElementById('toast-container').classList.add('success') : "nothing"
    var toast = document.createElement("div");
    toast.classList.add("custom__toast");
    toast.innerHTML = type == 1  ? success_icon +  `<span>${message}</span>`: error_icon  +  `<span>${message}</span>`;
    
    // Add the toast to the container
    var container = document.getElementById("toast-container");
    container.appendChild(toast);
    
    // Remove the toast after 5 seconds
      // setTimeout(function() {
      //   container.removeChild(toast);
      // }, 5000);
}
// toast notification function end

function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
      return false;
    return true;
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

