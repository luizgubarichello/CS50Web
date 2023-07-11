document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipient, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (subject === undefined) {
    recipient = '';
    subject = '';
    body = '';
  } else {
    if (subject.substring(0,3) !== 'RE:') {
      subject = 'RE: ' + subject;
    }
  }

  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

  // Send e-mail
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    load_mailbox('sent');
    return false;
  }

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load the appropriate mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // Create divs for each email
      for (email in emails) {
        const div = document.createElement('div');
        div.classList.add('row', 'p-1');
        div.id = emails[email].id;

        let Sender = emails[email].sender;
        let Subject = emails[email].subject;
        let TS = emails[email].timestamp;

        div.innerHTML = `<div class='col-3 font-weight-bold'>${Sender}</div>
        <div class='col-6'>${Subject}</div>
        <div class='col-3 text-right font-weight-light'>${TS}</div>`;
        div.style.border = 'thin solid';

        if (emails[email].read) {
          div.style.backgroundColor = "#cccccc";
        }

        div.addEventListener('click', () => {
          load_email(div.id);
          fetch(`/emails/${div.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          });
        });

        div.addEventListener('mouseover', () => {
          div.style.borderColor = '#007bff';
          div.style.cursor = 'pointer';
        })

        div.addEventListener('mouseleave', () => {
          div.style.borderColor = '#000000';
          div.style.cursor = 'default';
        })

        document.querySelector('#emails-view').append(div);
      }

  })
}

function load_email(email_id) {

  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear previously opened e-mail
  document.querySelector('#email-view').innerHTML = '';

  // Get the email
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // Show e-mail to user
      const div = document.createElement('div');
      div.classList.add('container-fluid');

      // Archival logic
      if (!email.archived) {
        btn_id = 'Archive';
      } else {
        btn_id = 'Unarchive';
      }

      div.innerHTML = `
      <div class='m-2 row'><button class='btn btn-outline-dark btn-sm' id='${btn_id}'>${btn_id}</button></div>
      <div class='m-2 row'><div class='p-0 col-2 font-weight-bold'>From: </div>${email.sender}</div>
      <div class='m-2 row'><div class='p-0 col-2 font-weight-bold text-left'>To: </div>${email.recipients}</div>
      <div class='m-2 row'><div class='p-0 col-2 font-weight-bold text-left'>Subject: </div>${email.subject}</div>
      <div class='m-2 row font-weight-light'>${email.timestamp}</div>
      <hr>
      <div class='m-2 row' style='white-space: pre-wrap;'>${email.body}</div>
      <div class='m-2 row'><button class='btn btn-outline-dark btn-sm' id='reply'>Reply</button></div>
      `;

      document.querySelector('#email-view').append(div);

      // Archive and unarchive e-mails
      btnElement = document.querySelector(`#${btn_id}`);

      if (userEmail === email.sender) {
        btnElement.setAttribute("hidden", "hidden");
      } else {
        btnElement.removeAttribute("hidden");
      }

      btnElement.addEventListener('click', () => {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        });

        load_mailbox('inbox');
      });

      // Reply e-mails
      document.querySelector('#reply').addEventListener('click', () => {
        replyBody = `\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`
        compose_email(email.sender, email.subject, replyBody)
      })

  });

}