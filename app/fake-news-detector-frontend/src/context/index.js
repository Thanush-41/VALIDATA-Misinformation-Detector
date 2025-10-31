import React, { Component } from 'react';

const MyContext = React.createContext();


class MyProvider extends Component { 

    state = {
        stage: 1,
        theme: localStorage.getItem('theme') || 'dark'
    }

    componentDidMount() {
        document.documentElement.setAttribute('data-theme', this.state.theme);
    }

    toggleTheme = () => {
        const themes = ['light', 'dark', 'blue', 'purple'];
        const currentIndex = themes.indexOf(this.state.theme);
        const nextIndex = (currentIndex + 1) % themes.length;
        const newTheme = themes[nextIndex];
        
        this.setState({ theme: newTheme }, () => {
            localStorage.setItem('theme', newTheme);
            document.documentElement.setAttribute('data-theme', newTheme);
        });
    }

    render() {
        return (
            <MyContext.Provider value={{
                state: this.state,
                toggleTheme: this.toggleTheme
            }}>
                {this.props.children}
            </MyContext.Provider>
        )
    }
}

export {MyContext, MyProvider}