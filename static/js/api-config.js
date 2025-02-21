// api-config.js
const apiConfig = {
    productionUrl: 'https://mister-kia-qrbozmensq-km.a.run.app',
    developmentUrl: 'http://localhost:8000',
    
    getBaseUrl() {
      const isLocalhost = window.location.hostname === 'localhost' || 
                         window.location.hostname === '127.0.0.1';
      const localPort = window.location.port || '8000';
      
      if (isLocalhost) {
        return `http://${window.location.hostname}:${localPort}`;
      }
      return this.productionUrl;
    }
  };
  
  // Make it globally available
window.apiConfig = apiConfig;