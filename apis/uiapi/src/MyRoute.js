import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Post2 from './Post2'
import Register from './Register'
import Login from './Login'

const MyRoute = () => {
    return (
        <>
            <Router>
                <Routes>
                    <Route path='/' element={<Post2 />} />
                    <Route path='/register' element={<Register />} />
                    <Route path='/login' element={<Login />} />


                </Routes>
            </Router>
        </>
    )
}

export default MyRoute