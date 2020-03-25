

const initial = {
    V: null,
    alpha: null,
    episodes: null
}

const app = (state = initial, action) => {
    switch(action.type){
        case 'UPDATE_V':
            return {...state, ...action.payload}
    }
    return state
}

export default app