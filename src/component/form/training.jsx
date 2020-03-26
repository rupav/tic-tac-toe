import React from 'react'
import { connect } from 'react-redux'
import axios from 'axios'
import { Formik, Form, Field } from 'formik'

import defaultParams from '../../axiosConfig'
import ActionType from '../../constant/ActionType'

const TrainRLAgent = (props) => {
    return(
        <div>
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
                    <Form className="form">
                        <label htmlFor="alpha" style={{ display: "block" }}>
                            Alpha
                        </label>
                        <Field
                            className="input"
                            type="number"
                            name="alpha"
                            placeholder=""
                        />
                        <label htmlFor="episodes" style={{ display: "block" }}>
                            Episode Count
                        </label>                        
                        <Field
                            className="input"
                            type="number"
                            name="episodes"
                            placeholder=""
                        />
                        <button className="form-button" type="submit" disabled={isSubmitting}>
                            Submit
                        </button>
                        <button className="modal-close" type="button" onClick={props.handleModal}>Close</button>
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