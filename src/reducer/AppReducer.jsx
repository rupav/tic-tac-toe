import ActionType from '../constant/ActionType'

const initial = {
    V: null,
    alpha: null,
    episodes: null
}

const app = (state = initial, action) => {
    switch(action.type){
        case ActionType.App.UPDATE_V:
            return {...state, ...action.payload}
        default:
            return state
    }
}

export default app