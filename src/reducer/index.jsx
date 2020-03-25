import { combineReducers } from 'redux'

import app from './AppReducer'

const Reducer = combineReducers({app})

const rootReducer = (state, action) => {
    return Reducer(state, action)
}

export default rootReducer