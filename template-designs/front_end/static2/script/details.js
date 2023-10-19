$(function () {
  // Get the hospital id from the query string parameters.
  const urlParams = new URLSearchParams(window.location.search);
  const hospitalId = urlParams.get('id');
  $('#btn-order-cards').click(function () {
    // Get id of the current user via the data-id attribute.
    let userId = $(this).attr('data-id');
    // Check weather the user is logged in or not.
    if (userId) {
      // Make an ajax call to get the current user information.
      $.ajax({
        url: `http://localhost:5001/api/v1/users/${userId}`,
        type: 'GET',
        contentType: 'application/json',
        success: function (response) {
          // Filter the uncompleted values of the current user attributes.
          result = Object.values(response).filter((value) => {
            return value === null || value === 'None';
          });
          // Check weather the profile of the current user is completed or not.
          if (result.length === 0) {
            const endpoint = `http://localhost:5001/api/v1/users/${userId}/orders`;
            // Make an ajax call to get the order information of the current user.
            $.ajax({
              url: endpoint,
              type: 'GET',
              contentType: 'application/json',
              success: function (response) {
                // Filter the orders of the current user linked to the current hospital.
                const checkOrder = response.filter((order) => {
                  return (
                    order.user_id == userId && order.hospital_id == hospitalId
                  );
                });
                // Check if the current user has card orders from the current hospital.
                if (checkOrder.length > 0) {
                  // If it has cards ordered, popup the corresponding error message.
                  $('#modal-error-message').text(
                    'You have cards in this hospital',
                  );
                  $('div#modalCompleteYourProfile').modal();
                } else {
                  // If the current user hasn't cards to the current hospital, we will register
                  // that user.
                  $.ajax({
                    type: 'POST',
                    url: endpoint,
                    contentType: 'application/json',
                    data: JSON.stringify({ hospital_id: hospitalId }),
                    success: function (response) {
                      const orderId = response.id;
                      // Check if the order is successfull
                      if (orderId) {
                        $('#modal-error-message').text(
                          'Your Order Is Successfull',
                        );
                        $('div#modalCompleteYourProfile').modal();
                      } else {
                        // If the order is not successfull by any means, we will popup
                        // some error message to the user
                        $('#modal-error-message').text(
                          'Something wrong happened',
                        );
                        $('div#modalCompleteYourProfile').modal();
                      }
                    },
                  });
                }
              },
            });
          } else {
            // If the profile is not completed, we will popup the corresponding
            // error message.
            $('#modal-error-message').text(
              'Please Complete Your Profile Before Ordering Cards',
            );
            $('div#modalCompleteYourProfile').modal();
          }
        },
      });
    } else {
      // If the user doesn't logged in, we will popup the corresponding message.
      $('#modal-error-message').text(
        'Please Login To Your Account Before Ordering Cards',
      );
      $('div#modalCompleteYourProfile').modal();
    }
  });
});
