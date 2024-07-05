function protectedCalls(tokenResponse) {
    const accessToken = tokenResponse.accessToken;
    return {

      getOrders: () => {
        const req = new Request("/signin");
        req.headers.set("Authorization", accessToken);
     return fetch(req)
      }
    }
  }
  
  const apiClient = protectedCalls(tokenResponse);
  apiClient.getOrders();
  