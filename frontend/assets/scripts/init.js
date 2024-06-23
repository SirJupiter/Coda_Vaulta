// const { options } = require('request');

class App {
  static #baseUrl = 'http://127.0.0.1:5000/api/';

  constructor() {
    this.registerOverlay = document.getElementById('register-overlay');
    this.registerForm = document.getElementById('registerForm');
    this.signInForm = document.getElementById('signInForm');
    this.signInOverlay = document.getElementById('sign-in-overlay');

    this.snippetSection = document.querySelector('#container-b section');
    this.cardContainer = '';
    this.originalCards = '';
    this.headerBoard = document.querySelector('.header-board');
    this.snippetDisplayBoard = document.querySelector('.snippet-display-board');
    this.snippetDisplay = document.querySelector('.snippet-display');

    this.snippetForm = document.getElementById('snippetForm');
    this.username = '';
    this.authToken = '';
    this.initEvents();
  }

  static getBaseUrl() {
    return App.#baseUrl;
  }

  initEvents() {
    // Check if user is already logged in
    this.checkIfLoggedIn();

    // Show registerOverlay
    document.querySelector('.register').addEventListener('click', () => {
      this.showRegisterOverlay();
    });

    // Hide registerOverlay when clicking outside the form
    this.registerOverlay.addEventListener('click', (event) => {
      if (event.target === this.registerOverlay) {
        this.hideRegisterOverlay();
      }
    });

    // Prevent the form from closing when it's clicked
    this.registerForm.addEventListener('click', (event) => {
      event.stopPropagation();
    });

    // Handle form submission
    this.registerForm.addEventListener('submit', (event) => {
      event.preventDefault();
      this.handleSubmit(event);
    });

    // Show signInOverlay
    document.querySelector('.sign-in').addEventListener('click', () => {
      if (this.isEmptyLocalStorage()) {
        this.showSignInOverlay();
      } else {
        this.handleSignOut();
      }
    });

    // Hide signInOverlay when clicking outside the form
    this.signInOverlay.addEventListener('click', (event) => {
      if (event.target === this.signInOverlay) {
        this.hideSignInOverlay();
      }
    });

    // Prevent the SignIn form from closing when it's clicked
    this.signInForm.addEventListener('click', (event) => {
      event.stopPropagation();
    });

    // Handle SignIn form submission
    this.signInForm.addEventListener('submit', (event) => {
      // event.preventDefault();
      this.handleSignIn(event);
    });

    // Prevent the snippet-creation form from closing when it's clicked
    this.snippetForm.addEventListener('click', (event) => {
      event.stopPropagation();
    });

    // Handle snippet form submission
    this.snippetForm.addEventListener('submit', (event) => {
      this.handleSnippetCreation(event);
    });
  }

  isEmptyLocalStorage() {
    return (
      localStorage.getItem('username') === null ||
      localStorage.getItem('authToken') === null
    );
  }

  fetchWithAuth(endpoint, options = {}) {
    // Set default header for Fetch API when logged in
    if (this.authToken) {
      options.headers = options.headers || {};

      options.headers['Authorization'] = this.authToken;
    }
    const url = `${App.#baseUrl}${endpoint}`;
    return fetch(url, options);
  }

  checkIfLoggedIn() {
    if (!this.isEmptyLocalStorage() || !this.isLoggedIn()) {
      const username = localStorage.getItem('username');
      const authToken = localStorage.getItem('authToken');
      if (username && authToken) {
        this.username = username;
        this.authToken = authToken;

        this.checkTokenValidity()
          .then((data) => {
            console.log('Success:', data);
            if (this.isLoggedIn()) {
              const welcome = document.createElement('div');
              welcome.textContent = `Welcome,  ${this.username} 😎🎉`;
              Object.assign(welcome.style, {
                color: 'white',
                fontSize: '1.5rem',
                marginTop: '0.7rem',
                letterSpacing: '6px',
                textAlign: 'right',
              });

              document.querySelector('nav').after(welcome);
              document.querySelector('.sign-in').textContent = 'Logout';
              document.querySelector('.register').style.display = 'none';

              this.showSnippetDisplayBoard();
              this.displaySnippets();
              this.showCreateSnippetForm();
            }
          })
          .catch((error) => {
            console.error('Token validation error:', error);
            localStorage.removeItem('username');
            localStorage.removeItem('authToken');
            window.location.href = '/frontend/index.html';
            // document.querySelector('.sign-in').textContent = 'Sign In';
            // document.querySelector('.register').style.display = 'inline-block';
            // document.querySelector('nav').nextElementSibling.remove();
          });
      }
    }
  }

  async checkTokenValidity() {
    const response = await this.fetchWithAuth('protected', { method: 'GET' });

    const responseData = await response.json();

    if (response.ok) {
      return responseData;
    } else {
      throw new Error(responseData.msg || 'Token expired or invalid');
    }
  }

  showRegisterOverlay() {
    this.registerOverlay.style.display = 'flex';
    // $('.register-overlay,.drop').fadeIn("slow");

    document.querySelector('.success').style.display = 'none';
    document.querySelector('.drop').style.display = 'flex';
  }

  showSignInOverlay() {
    // $('.sign-in-overlay,.in-drop').fadeIn("slow");
    this.signInOverlay.style.display = 'flex';
    const inDropElement = document.querySelector('.in-drop');
    inDropElement.style.display = 'flex';
  }

  hideRegisterOverlay() {
    this.registerOverlay.style.display = 'none';
    // $('.register-overlay, .drop').fadeOut("slow");
  }

  hideSignInOverlay() {
    this.signInOverlay.style.display = 'none';
    // $('.sign-in-overlay, .in-drop').fadeOut("slow");
  }

  handleSubmit(event) {
    event.preventDefault();

    // Collect form data
    const formData = new FormData(this.registerForm);
    const data = {
      username: formData.get('name'),
      email: formData.get('email'),
      password: formData.get('password'),
    };

    // Send the data using fetch to the CodaVaulta API endpoint
    fetch(`${App.#baseUrl}user/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (!response.ok) {
          throw new Error(responseData.error || 'Cannot register: Try again');
        }
        return responseData;
      })
      .then((data) => {
        console.log(data);

        document.querySelector('.success').style.display = 'flex';
        document.querySelector('.drop').style.display = 'none';

        setTimeout(() => {
          this.hideRegisterOverlay();
        }, 3000);

        this.registerForm.reset();
      })
      .catch((error) => {
        console.error('Error:', error.message);
        // Handle errors here
        const errorMessage = document.createElement('h4');
        errorMessage.textContent = error.message;
        errorMessage.style.color = 'red';
        this.registerForm
          .querySelector('.input-box:last-child')
          .before(errorMessage);

        setTimeout(() => {
          errorMessage.remove();
        }, 3000);
      });
  }

  handleSignIn(event) {
    event.preventDefault(); // Prevent the default form submission

    // Collect form data
    const formData = new FormData(this.signInForm);
    const data = {
      email: formData.get('email'),
      password: formData.get('password'),
    };

    // Send the data using fetch to the CodaVaulta API endpoint
    fetch(`${App.#baseUrl}user/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (!response.ok) {
          throw new Error(responseData.error || 'Cannot sign in: Try again');
        }
        return responseData;
      })
      .then((data) => {
        console.log(data);
        this.username = data.username;
        this.authToken = `Bearer ${data.authentication_token}`;
        this.hideSignInOverlay();
        this.signInForm.reset();

        // Store the username and authToken in the localStorage
        localStorage.setItem('username', this.username);
        localStorage.setItem('authToken', this.authToken);

        if (this.isLoggedIn()) {
          const welcome = document.createElement('div');
          welcome.textContent = `Welcome,  ${this.username} 😎🎉`;
          Object.assign(welcome.style, {
            color: 'white',
            fontSize: '1.5rem',
            marginTop: '0.7rem',
            letterSpacing: '6px',
            textAlign: 'right',
          });

          document.querySelector('nav').after(welcome);
          document.querySelector('.sign-in').textContent = 'Logout';
          document.querySelector('.register').style.display = 'none';

          this.showSnippetDisplayBoard();
          this.displaySnippets();
          this.showCreateSnippetForm();
        }
      })
      .catch((error) => {
        console.error('Error:', error.message);

        const errorMessage = document.createElement('h4');
        errorMessage.textContent = error.message;
        errorMessage.style.color = 'red';
        this.signInForm
          .querySelector('.in-input-box:last-child')
          .before(errorMessage);

        setTimeout(() => {
          errorMessage.remove();
        }, 3000);
      });
  }

  handleSignOut() {
    // Handles sign out operation
    this.fetchWithAuth('user/logout', { method: 'POST' })
      .then(async (response) => {
        const responseData = await response.json();
        if (!response.ok) {
          throw new Error(responseData.error || 'Cannot sign out: Try again');
        }
        return responseData;
      })
      .then((data) => {
        console.log(data);
        this.username = '';
        this.authToken = '';
        localStorage.removeItem('username');
        localStorage.removeItem('authToken');
        document.querySelector('.sign-in').textContent = 'Sign In';
        document.querySelector('.register').style.display = 'inline-block';
        document.querySelector('nav').nextElementSibling.remove();

        this.hideSnippetDisplayBoard();
        this.removeDisplaySnippets();
        this.hideCreateSnippetForm();
        this.snippetForm.reset();
      })
      .catch((error) => {
        console.error('Error:', error.message);
      });
  }

  handleSnippetCreation(event) {
    event.preventDefault();
    const formData = new FormData(this.snippetForm);
    const snippet = {
      title: formData.get('title'),
      description: formData.get('description'),
      language: formData.get('language'),
      code: formData.get('code'),
    };

    this.createSnippet(snippet)
      .then((data) => {
        console.log(data);

        this.renderSnippetOnSnippetBoard(data);
        this.displaySnippets();

        this.snippetForm.reset();
      })
      .catch((error) => {
        console.error(error.message);

        const errorMessage = document.createElement('h4');
        errorMessage.textContent = error.message;
        errorMessage.style.color = 'red';
        errorMessage.style.fontWeight = 'normal';
        errorMessage.style.fontSize = '16px';
        this.snippetForm
          .querySelector('.input-bx:last-child')
          .before(errorMessage);

        setTimeout(() => {
          errorMessage.remove();
        }, 3000);
      });
  }

  renderSnippetOnSnippetBoard(snippet) {
    const { title, code, description, language } = snippet;

    // Create the title element
    if (title) {
      const titleElement = document.querySelector('.snippet-display-header h5');
      titleElement.textContent = title;
    }

    // Create the description element
    if (description) {
      const descriptionElement = document.querySelector('.snippet-desc');
      descriptionElement.textContent = description;
    }

    const codeBlock = document.querySelector('.snippet-display-body code');

    codeBlock.classList.add(`language-${language}`); // Use the detected language for the class
    codeBlock.textContent = code;
    Prism.highlightElement(codeBlock);

    // Display the detected language
    const languageElement = document.querySelector('.snippet-language');
    languageElement.textContent = language;

    const downloadBtn = document.querySelector('.download');
    downloadBtn.onclick = () =>
      this.downloadSnippetAsImage(code, title || 'snippet');

    const editBtn = document.querySelector('.edit');
    editBtn.onclick = () => {};

    const deleteBtn = document.querySelector('.delete');

    deleteBtn.addEventListener('click', () => {
      this.showDeleteSnippetConfirmationModal(snippet);
    });

    // Append the snippet container to the snippet board
    this.snippetDisplay.style.display = 'block';
    this.snippetDisplayBoard.style.display = 'block';
  }

  showDeleteSnippetConfirmationModal(snippet) {
    $('.modalcontainer,.modal').fadeIn('slow');

    $('.close,.buttons a:first-child').click(function () {
      $('.modalcontainer,.modal').fadeOut('slow');
    });

    const yesButton = document.querySelector('.buttons a:last-child');
    const noButton = document.querySelector('.buttons a:first-child');

    // Remove existing event listeners to prevent duplication
    yesButton.removeEventListener('click', this.yesButtonHandler);

    // Create a new handler function that can be removed later
    this.yesButtonHandler = (event) => {
      this.deleteSnippet(snippet)
        .then((data) => {
          console.log(data);
          $('.modalcontainer,.modal').fadeOut('slow');
          this.snippetDisplay.style.display = 'none';
          this.displaySnippets();
        })
        .catch((error) => {
          console.error(error.message);
          document.querySelector('.modalcontainer p').textContent =
            'Oops! Something went wrong';
          document.querySelector('.modalcontainer p').style.color = 'red';
          document.querySelector('.modalcontainer .buttons').style.display =
            'none';
          document.querySelector('.modalcontainer h3').style.display = 'none';

          setTimeout(() => {
            $('.modalcontainer,.modal').fadeOut('slow');
          }, 3000);

          document.querySelector('.modalcontainer p').textContent =
            'Are you sure you want to delete this snippet? Snippets delete cannot be retrieved anymore after deletion. Please confirm.';
          document.querySelector('.modalcontainer p').style.color =
            'var(--medium-dark)';
          document.querySelector('.modalcontainer .buttons').style.display =
            'block';
          document.querySelector('.modalcontainer h3').style.display = 'block';
        });
    };

    // Attach the new event listener
    yesButton.addEventListener('click', this.yesButtonHandler);

    // Close popup when clicking the esc keyboard button
    document.addEventListener('keyup', function (event) {
      if (event.key === 'Escape') {
        $('.modalcontainer,.modal').fadeOut('slow');
      }
    });
  }

  downloadSnippetAsImage(code, filename) {
    // Create a canvas element
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');

    // Set canvas background (optional)
    ctx.fillStyle = '#fff'; // White background
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Prepare text
    ctx.fillStyle = '#000';
    ctx.font = '16px monospace';
    const lines = code.split('\n');
    let startY = 20; // Start position for the text

    // Draw text onto canvas
    lines.forEach((line) => {
      ctx.fillText(line, 10, startY); // Adjust positioning as needed
      startY += 20; // Line height
    });

    // Convert canvas to JPEG URL
    const imageURL = canvas.toDataURL('image/jpeg');

    // Trigger download
    const link = document.createElement('a');
    link.href = imageURL;
    link.download = `${filename}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  isLoggedIn() {
    // Check to be sure if a user is already logged in
    return this.username !== '' && this.authToken !== '';
  }

  // SNIPPET MANAGEMENT
  async fetchSnippets() {
    const response = await this.fetchWithAuth('user/get_snippets', {
      method: 'GET',
    });

    const data = await response.json();
    if (response.ok) {
      return data;
    } else {
      throw new Error(data.error || 'Failed to fetch snippets');
    }
  }

  async createSnippet(snippet) {
    const response = await this.fetchWithAuth('user/create_snippet', {
      method: 'POST',
      headers: {
        'content-Type': 'application/json',
      },
      mode: 'cors',
      body: JSON.stringify(snippet),
    });

    const data = await response.json();
    if (response.ok) {
      return data;
    } else {
      throw new Error(data.error || 'Failed to create snippet');
    }
  }

  async updateSnippet(snippet) {
    const response = await this.fetchWithAuth('user/update_snippet', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(snippet),
    });

    const responseData = await response.json();
    if (response.ok) {
      return responseData;
    } else {
      throw new Error(responseData.error || 'Failed to update snippet');
    }
  }

  async deleteSnippet(snippet) {
    const response = await this.fetchWithAuth('user/delete_snippet', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(snippet),
    });

    const responseData = await response.json();
    if (response.ok) {
      return responseData;
    } else {
      throw new Error(responseData.error || 'Failed to delete snippet');
    }
  }

  // Display user snippet at login or no snippets message if user has none
  displaySnippets() {
    if (!this.isEmptyLocalStorage() && this.isLoggedIn()) {
      this.fetchSnippets()
        .then((snippets) => {
          console.log(snippets);

          const cards = Array.from(document.getElementsByClassName('cards'));
          const originalCards = [...cards];
          this.originalCards = originalCards;

          if (snippets.length > 0) {
            this.displaySnippetsList(snippets);
          } else {
            const message = `${this.username}, you have no snippets yet.`;
            this.displayNoSnippetsMessage(message);
          }
        })
        .catch((error) => {
          console.error(error.message);
        });
    }
  }

  displayNoSnippetsMessage(message) {
    // Remove all child of snippetSection
    this.snippetSection.innerHTML = '';

    // Create and append error message
    const errorMessage = document.createElement('h5');
    errorMessage.textContent = message;
    errorMessage.style.color = 'white';
    errorMessage.style.fontWeight = 'normal';
    this.snippetSection.appendChild(errorMessage);

    Object.assign(this.snippetSection.style, {
      display: 'flex',
      textAlign: 'center',
      alignItems: 'center',
      justifyContent: 'center',
    });
  }

  displaySnippetsList(snippets) {
    // Remove all child of snippetSection
    // while (this.snippetSection.lastChild) {
    //   this.snippetSection.lastChild.style.display = 'none';
    // }
    this.snippetSection.innerHTML = '';
    Object.assign(this.snippetSection.style, {
      display: 'block',
      textAlign: 'unset',
      alignContent: 'unset',
      overflow: 'auto',
      width: '90%',
      margin: '0 auto',
    });

    const cardContainer = document.createElement('div');
    cardContainer.classList.add('card-container', 'snaps-inline');

    // Create and append the snippet cards
    snippets.forEach((snippet) => {
      const card = this.createSnippetCard(snippet);

      card.addEventListener('click', () =>
        this.renderSnippetOnSnippetBoard(snippet)
      );
      cardContainer.appendChild(card);
    });

    this.snippetSection.appendChild(cardContainer);
    // this.cardContainer = cardContainer;
  }

  createSnippetCard(snippet) {
    const card = document.createElement('div');
    card.classList.add('card', 'inconsolata-text');

    const title = document.createElement('h5');
    title.className = 'card-title';
    title.textContent = snippet.title;

    const created = document.createElement('p');
    created.className = 'card-created';
    created.textContent = `Created: ${snippet.updated_at}`;

    card.appendChild(title);
    card.appendChild(created);

    return card;
  }

  showCreateSnippetForm() {
    // Show the create snippet form
    document.querySelector('.header-icon').style.display = 'none';
    document.querySelector('.create-snippet-form').style.display = 'flex';
  }

  hideCreateSnippetForm() {
    // Hide the create snippet form
    document.querySelector('.header-icon').style.display = 'flex';
    document.querySelector('.create-snippet-form').style.display = 'none';
  }

  showSnippetDisplayBoard() {
    this.headerBoard.style.display = 'none';
    this.snippetDisplayBoard.style.display = 'block';
  }

  hideSnippetDisplayBoard() {
    this.headerBoard.style.display = 'block';
    this.snippetDisplayBoard.style.display = 'none';
  }

  removeDisplaySnippets() {
    this.snippetSection.innerHTML = '';
    this.originalCards.forEach((card) => {
      this.snippetSection.appendChild(card);
    });

    // this.cardContainer.remove();
    // while (this.snippetSection.lastChild) {
    //   this.snippetSection.lastChild.style.display = 'flex';
    // }
    Object.assign(this.snippetSection.style, {
      display: 'grid',
      textAlign: 'unset',
      alignContent: 'unset',
    });
  }
}

// Instantiate the App class when the document is ready
document.addEventListener('DOMContentLoaded', () => {
  new App();
});
