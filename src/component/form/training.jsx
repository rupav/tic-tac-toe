import React from 'react'
import { connect } from 'react-redux'
import axios from 'axios'
import { Formik, Form, Field } from 'formik'

import defaultParams from '../../axiosConfig'
import ActionType from '../../constant/ActionType'

const TrainRLAgent = (props) => {
    return(
        <div>
            <span className="modal-close" onClick={props.handleModal}>x</span>
            <Formik
                initialValues = {{ alpha: "", episodes: "" }}
                onSubmit = {(values, {setSubmitting, resetForm}) => {
                    const params = {alpha: values.alpha/100, episodes: values.episodes}
                    console.log(params)
                    axios({
                        ...defaultParams,
                        url: '/train',
                        data: params
                    }).then((resp) => {
                        console.log(resp.data)
                        const action = {
                            type: ActionType.App.UPDATE_V,
                            payload: resp.data
                        }
                        setSubmitting(false)
                        resetForm()
                        props.dispatch(action)
                        console.log('Action dispatched!')
                    }).catch((error) => {
                        console.log(error)
                        setSubmitting(false)
                        resetForm()
                    });
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
    return app
}

export default connect(mapStateToProps)(TrainRLAgent)