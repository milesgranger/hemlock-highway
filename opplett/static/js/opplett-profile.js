/**
 * Created by milesg on 20.05.17.
 */

$(document).ready(function(){

    // Make directory button click logic
    $('#new_dir_button').click(function(){

        // Hide any other forms if they are visible.
        if ($('#rm_dir_form').is(":visible")){
            $('#rm_dir_form').toggle(250);
        }
        $('#new_dir_form').toggle(500);
    });

    // Remove directory button click logic
    $('#rm_dir_button').click(function(){

        // Hide any other forms if they are visible.
        if ($('#new_dir_form').is(":visible")){
            $('#new_dir_form').toggle(250);
        }
        $('#rm_dir_form').toggle(500);
    });


});
