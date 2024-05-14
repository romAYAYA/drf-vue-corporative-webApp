import axios from 'axios'

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response ? error.response.status : null
    console.log('error', error)
    if (error.response) {
      const noTokenProvided =
        error.response.data.detail === 'No refresh token provided'
      const invalidRefreshToken =
        error.response.data.detail === 'Invalid refresh token'

      if (status === 401 && !noTokenProvided && !invalidRefreshToken) {
        return refreshToken().then((_) => {
          console.log('got refresh token')
          return axios.request(error.config)
        })
      }
    } else {
      console.log('probably got 500 error:', error)
    }

    return Promise.reject(error)
  },
)
