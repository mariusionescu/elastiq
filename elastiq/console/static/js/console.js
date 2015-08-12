/**
 * Created by marius on 07/08/15.
 */

$(document).ready(function () {
    $("#addNode").click(function () {
        $('.ui.modal')
            .modal({
                blurring: true
            })
            .modal('show')
        ;
    });
    $("#addNodeCancel").click(function (){
        $('.ui.modal').modal("hide");
    })
});

function confirm_delete(name) {
  return confirm('Are you sure node ' + name +'?');
};
