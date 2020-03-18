import React from 'react';
import axios from 'axios';
import { Formik, Form, Field } from 'formik';

const TrainRLAgent = () => {
    return(
        <div>
            <Formik
                initialValues = {{ alpha: "", episodes: "" }}
                onSubmit = {(values, {setSubmitting}) => {
                    const url = "https://rupav-tic-tac-toe.herokuapp.com/api/train"
                    const params = {alpha: values.alpha/100, episodes: values.episodes}
                    console.log(params)
                    axios({
                        method: 'post',
                        url: url,
                        crossdomain: true,
                        data: params,
                        headers: {
                            "Content-type": "application/json"
                        }
                    }).then((resp) => {
                        console.log(resp.data)
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

export default TrainRLAgent