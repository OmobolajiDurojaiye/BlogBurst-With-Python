<!DOCTYPE html>
<html>
<head>
	<title>Test</title>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
</head>
<body>

  <!-- Button trigger modal -->
<button type="button" class="btn btn-primary mybtn" data-toggle="modal" data-target="#exampleModal" data-user='56'>  View Details of User 56 </button>
 
<button type="button" class="btn btn-primary mybtn" data-toggle="modal" data-target="#exampleModal" data-user='34'> View Details of User 34</button>


<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/bootstrap.min.js"></script>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>

<script type="text/javascript"> 

//triggered when modal is about to be shown
$('#exampleModal').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var userid = $(e.relatedTarget).data('user');
    alert(userid);
    //make an ajax call to receive an array based on userid, that is you can now pass the userid to an ajax. let's say the ajax returns t     

    $(e.currentTarget).find('.modal-body').html(t); //displays t inside the div with class modal-body
    $(e.currentTarget).find('.modal-title').html("Details for User"+ userid); //displays this in the div with class modal-title

});
</script>

</body>
</html>