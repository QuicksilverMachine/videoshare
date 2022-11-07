import {SERVER_URL} from './config'


const ExplorePath = `${SERVER_URL}/explore`
const FolderPath = `${SERVER_URL}/folder`
const VideoPath = `${SERVER_URL}/video`


function get(url) {
    return fetch(url).then( (response) => response.json() );
}

function post(url, body) {
    const requestMetadata = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    };
    return fetch(url, requestMetadata).then( (response) => response.json() );
}

function patch(url, body) {
    const requestMetadata = {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    };
    return fetch(url, requestMetadata).then( (response) => response.json() );
}

export function ResolvePath() {
    return get(`${ExplorePath}${window.location.pathname}`);
}

export function GetFolder(folder_id) {
    return get(`${FolderPath}/${folder_id}`);
}

export function CreateFolder(name, parent_id) {
    return post(`${FolderPath}/`, {"name": name, "parent_id": parent_id})
}

export function MoveFolder(folder_id, parent_id) {
    return patch(`${FolderPath}/${folder_id}`, {"parent_id": parent_id})
}

export function CreateVideo(name, parent_id) {
    return post(`${VideoPath}/`, {"name": name, "parent_id": parent_id})
}

export function MoveVideo(folder_id, parent_id) {
    return patch(`${VideoPath}/${folder_id}`, {"parent_id": parent_id})
}
