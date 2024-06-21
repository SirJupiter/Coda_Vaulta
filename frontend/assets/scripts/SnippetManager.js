import App from './init.js';

class SnippetManager extends App {
  constructor() {
    super();
    this.baseUrl = App.getBaseUrl();
    this.initEvents();
  }

  initEvents() {
    // super.initEvents();
  }

  async fetchSnippets() {
    const response = await this.fetchWithAuthtch('user/get_snippets', {
      method: 'GET',
    });

    const data = await response.json();
    if (response.ok) {
      console.log(data);
      return data;
    } else {
      throw new Error(data.error || 'Failed to fetch snippets');
    }
  }

  async createSnippet(snippet) {
    const response = await this.fetchWithAuth('user/create_snippet', {
      method: 'POST',
      body: JSON.stringify(snippet),
    });

    const data = await response.json();
    if (response.ok) {
      console.log(data);
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
      console.log(responseData);
      return responseData;
    } else {
      throw new Error(responseData.error || 'Failed to update snippet');
    }
  }

  async deleteSnippet() {
    const response = await this.fetchWithAuth('user/delete_snippet', {
      method: 'DELETE',
    });

    const responseData = await response.json();
    if (response.ok) {
      return responseData;
    } else {
      throw new Error(responseData.error || 'Failed to delete snippet');
    }
  }

  displaySnippets() {
    if (!this.isEmptyLocalStorage() && this.isLoggedIn()) {
      this.fetchSnippets()
        .then((snippets) => {
          console.log(snippets);
        })
        .catch((error) => {
          console.error(error.messae);
          // const errorMessage = error.me
        });
    }
  }
}

export default SnippetManager;
