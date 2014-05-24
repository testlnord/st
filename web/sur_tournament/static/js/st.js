/**
 * Created by arkady on 5/24/14.
 */
$("button[name='log']").click(function(){
    var gamid;
    gamid_ = $(this).attr("data-gameid");
    tour_ = $(this).attr("data-torid");
    game_view_id = "#game_log".concat(tour_)
    $.get("/game_log/", {gamid: gamid_ }, function(data){
        $(game_view_id).html(data);
        $(game_view_id).show();
    });
});
