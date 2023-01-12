function toggleDropdown() {
    document.getElementById("myDropdown").classList.add("show");
}

window.onclick = function(event) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    if (!event.target.matches('.dropdownbutton')) {

        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

document.getElementById("myDropdown").addEventListener('click',function(event){
    event.stopPropagation();
});

function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByClassName("other-birds-input");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].value
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}