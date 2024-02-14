import React from 'react'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { API } from './config'
import Register from './Register'


const Post2 = () => {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        axios.get(`${API}/post`)
            .then(res => setPosts(res.data))
            .catch(err => console.log(err))
    }, [])
    return (
        <>
            {posts.map((item, i) => (
                <div key={i}>
                    <h1>Title:{item.title}</h1>
                    <p>URL:{item.url}</p>
                </div>
            ))}
            {/* <Register /> */}

        </>
    )
}

export default Post2



