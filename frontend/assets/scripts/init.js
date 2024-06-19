// const { options } = require('request');

class App {
  static #baseUrl = 'http://127.0.0.1:5000/api/';

  constructor() {
    this.registerOverlay = document.getElementById('register-overlay');
    this.registerForm = document.getElementById('registerForm');
    this.signInForm = document.getElementById('signInForm');
    this.signInOverlay = document.getElementById('sign-in-overlay');
    this.username = '';
    this.authToken = '';
    this.initEvents();
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
    if (!this.isEmptyLocalStorage()) {
      const username = localStorage.getItem('username');
      const authToken = localStorage.getItem('authToken');
      if (username && authToken) {
        this.username = username;
        this.authToken = authToken;
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
      }
    }
  }

  showRegisterOverlay() {
    this.registerOverlay.style.display = 'flex';
    // this.signInOverlay.style.display = 'none';
    document.querySelector('.success').style.display = 'none';
    document.querySelector('.drop').style.display = 'flex';
    // this.registerForm.reset();
  }

  showSignInOverlay() {
    this.signInOverlay.style.display = 'flex';
    // this.registerOverlay.style.display = 'none';
    const inDropElement = document.querySelector('.in-drop');
    console.log('in-drop element:', inDropElement); // Verify the element is selected correctly
    inDropElement.style.display = 'flex';
    // document.querySelector('.in-drop').style.display = 'flex';
  }

  hideRegisterOverlay() {
    this.registerOverlay.style.display = 'none';
  }

  hideSignInOverlay() {
    this.signInOverlay.style.display = 'none';
  }

  handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

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
        const errorMessage = document.createElement('h3');
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
      })
      .catch((error) => {
        console.error('Error:', error.message);
        // Handle errors here
        const errorMessage = document.createElement('h3');
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
        localStorage.removeItem('username');
        localStorage.removeItem('authToken');
        document.querySelector('.sign-in').textContent = 'Sign In';
        document.querySelector('.register').style.display = 'inline-block';
        document.querySelector('nav').nextElementSibling.remove();
      })
      .catch((error) => {
        console.error('Error:', error.message);
      });
  }
}

// Instantiate the SignUpOverlay class when the document is ready
document.addEventListener('DOMContentLoaded', () => {
  new App();

});
