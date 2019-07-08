$('.custom-file-input').on('change', function() { 
   let fileName = $(this).val().split('\\').pop(); 
   console.log(fileName)
   $(this).next('.custom-file-label').addClass("selected").html(fileName); 
});
