//* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content
var dropdown = document.getElementsByClassName("dropdown-link");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.add("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}

let myLabels = document.querySelectorAll('.lbl-toggle'); Array.from(myLabels).forEach(label => { 
  label.addEventListener('keydown', e => { if (e.which === 32 || e.which === 13) 
    { 
      e.preventDefault(); label.click(); 
    }; 
  }); 
}); 

