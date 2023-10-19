$(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get('user_id');
  $('button#hide-order-listings').click(function () {
    if ($('div#order-tobe-hided').hasClass('order-hider')) {
      $('div#order-tobe-hided').removeClass('order-hider');
    } else {
      $('div#order-tobe-hided').addClass('order-hider');
    }
  });

  const firstName = $('#firstName');
  const lastName = $('#lastName');
  const country = $('#country');
  const state = $('#state');
  const city = $('#city');
  const age = $('#age');
  const sex = $('#sex');
  const birthPlace = $('#birthPlace');

  $('button#hide-order-listings').click(function () {
    $('ul.card-list').empty();
    const endpoint = `http://localhost:5001/api/v1/users/${userId}/orders`;
    $.ajax({
      url: endpoint,
      type: 'GET',
      contentType: 'application/json',
      success: function (response) {
        if (response.length > 0) {
          response.forEach((order) => {
            $.ajax({
              url: `http://localhost:5001/api/v1/hospitals/${order.hospital_id}`,
              type: 'GET',
              contentType: 'application/json',
              success: function (response) {
                $('ul.card-list').append(`<li>${response.name}</li>`);
              },
            });
          });
        } else {
          $('h3#change-me-if-no-orders').text(`You don't have cards yet!`);
        }
      },
    });
  });
  $('button#btn-profile-change').click(function () {
    const profileData = {
      first_name: firstName.val(),
      last_name: lastName.val(),
      country: country.val(),
      state: state.val(),
      city: city.val(),
      age: age.val(),
      sex: sex.val(),
      place_of_birth: birthPlace.val(),
    };
    $.ajax({
      url: `http://0.0.0.0:5001/api/v1/users/${userId}`,
      type: 'PUT',
      contentType: 'application/json',
      data: JSON.stringify(profileData),
      success: function (data) {
        location.reload(true);
      },
    });
    return false;
  });
});
