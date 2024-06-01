console.log("hello");

function append_book_items(book_list, admin = false) {
  let parent = document.querySelector(".books");
  parent.innerHTML = "";
  for (book of book_list) {
    let book_element = `
    <li class="${admin ? `admin-list-items` : `list-items`}">
      <span>${book[1]}</span>
      <span>${book[2]}</span>
      <span>${book[3]}</span>
      ${
        admin
          ? `<span>${book[4]}</span> <span> <form> <input class= "restock-${book[0]}" type = "number" required placeholder="Enter Quantity"> <button onclick="handleRestock(event, '${book[4]}', '${book[0]}')">Restock</button> </form> </span>`
          : `<span><button class="buttons" onclick="window.location.href='/issuebooks.html?book=${book[1]}'">Issue</button></span>`
      }
    </Li>
    `;
    parent.innerHTML += book_element;
  }
}

var url_string = window.location.href;
var url = new URL(url_string);
var book = url.searchParams.get("book");
document.querySelector(".form-book").innerHTML = `Book: ${book}`;

function handleAdminAccess(event) {
  event.preventDefault();
  let password = document.querySelector(".admin-pass").value;
  console.log(password);

  eel
    .check_pass(password)()
    .then(function (res) {
      res
        ? (window.location.href = "/admin.html")
        : alert("WRONG PASSWORD ENTERED!");
    });

  document.querySelector(".admin-pass").value = "";
}

function handleIssueBook(event) {
  event.preventDefault();

  let name = document.querySelector(".username").value;
  console.log(name);

  eel
    .issue_book(name, book)()
    .then((res) => console.log(res));
  alert("Book Has Been Issued. Pick it from the counter");
}

function handleAddBook(event) {
  event.preventDefault();
  let book_name = document.querySelector(".book_name").value;
  console.log(book_name);

  let genre = document.querySelector(".genre").value;
  console.log(genre);

  let fine = Number(document.querySelector(".fine").value);
  console.log(fine);

  let quantity = Number(document.querySelector(".book_quantity").value);
  console.log(quantity);

  eel
    .add_book(book_name, genre, fine, quantity)()
    .then((res) => console.log(res));
  location.reload();
}

function handleRestock(event, quantity, bookId) {
  event.preventDefault();
  let newQuantity = Number(document.querySelector(`.restock-${bookId}`).value);
  eel
    .restock(newQuantity + Number(quantity), bookId)()
    .then((res) => console.log(res));
  location.reload();
}
