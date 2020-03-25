import React from 'react'
import { connect } from 'react-redux'
import axios from 'axios'
import { Formik, Form, Field } from 'formik'
import defaultParams from './axiosConfig'

const TrainRLAgent = (props) => {
    return(
        <div>
            <Formik
                initialValues = {{ alpha: "", episodes: "" }}
                onSubmit = {(values, {setSubmitting}) => {
                    const params = {alpha: values.alpha/100, episodes: values.episodes}
                    console.log(params)
                    axios({
                        ...defaultParams,
                        url: '/train',
                        data: params
                    }).then((resp) => {
                        console.log(resp.data)
                        const action = {
                            type: 'UPDATE_V',
                            payload: resp.data
                        }
                        props.dispatch(action)
                        console.log('Action dispatched!')
                    }).catch((error) => {
                        console.log(error)
                    });
                    setSubmitting = true
                }}
            >
                {({ isSubmitting }) => (
                    <Form>
                        <Field
                            type="number"
                            name="alpha"
                            placeholder="Alpha"
                        />
                        <Field
                            type="number"
                            name="episodes"
                            placeholder="Episodes count"
                        />
                        <button type="submit" disabled={isSubmitting}>
                            Submit
                        </button>
                    </Form>
                )}            
            </Formik>
        </div>
    );
}

const mapStateToProps = (state, props) => {
    const app = state.app
    return {
        V: app.V
    }
}

export default connect(mapStateToProps)(TrainRLAgent)