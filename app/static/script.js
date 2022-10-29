let api_url = "/api"

async function getAPIInstanceID() {
    let response = await fetch('/api')
    let json = await response.json()
    return json
}

async function getJoke() {
    let response = await fetch('/joke')
    let json = await response.json()
    return json
}

function setAPIInstanceIDOnPage(id) {
    let text
    if (id) {
        text = "Connected to backend server instance: " + id
    } else {
        text = `Unable to connect to backend server instance at URL (${api_url}). Please refresh to try again.`
    }
    document.getElementById("instance_id").innerText = text
}

function setJokeOnPage(joke) {
    let text
    if (joke) {
        text = joke.setup + " " + joke.punchline
    } else {
        text = `Unable to retreive joke from 3rd party API`
    }
    document.getElementById("joke").innerText = text
}

async function main() {
    let instance_id_data = await getAPIInstanceID()
    setAPIInstanceIDOnPage(instance_id_data.server_details?.server_instance_id)

    let joke_data = await getJoke()
    setJokeOnPage(joke_data.joke)
}

main()