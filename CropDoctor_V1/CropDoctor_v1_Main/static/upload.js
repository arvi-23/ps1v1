// function readURL(input) {
//     if (input.files && input.files[0]) {
//         var reader = new FileReader();
      
//         reader.onload = function (e) {
//             $('#blah')
//                 .attr('src', e.target.result)
//                 .width(150)
//                 .height(200);
//         };
      
//         reader.readAsDataURL(input.files[0]);
//     }
//     }


//     $(document).ready(function () {
//         // Init
//         $('.image-section').hide();
//         $('.loader').hide();
//         $('#result').hide();
    
//         // Upload Preview
//         function readURL(input) {
//             if (input.files && input.files[0]) {
//                 var reader = new FileReader();
//                 reader.onload = function (e) {
//                     $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
//                     $('#imagePreview').hide();
//                     $('#imagePreview').fadeIn(650);
//                 }
//                 reader.readAsDataURL(input.files[0]);
//             }
//         }
//         $("#imageUpload").change(function () {
//             $('.image-section').show();
//             $('#btn-predict').show();
//             $('#result').text('');
//             $('#result').hide();
//             readURL(this);
//         });
//     });