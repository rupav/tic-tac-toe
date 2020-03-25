const defaultParams = {
    baseURL: process.env.REACT_APP_API_URI,
    method: 'post',
    crossdomain: true,
    data: null,
    headers: {
        "Content-type": "application/json"
    }
}

export default defaultParams