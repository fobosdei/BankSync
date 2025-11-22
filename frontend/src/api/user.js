import axios from 'axios';

export const apiRegister = (data) => axios.post('/users', data);
export const apiGetUserList = () => axios.get('/users');
export const apiUpdateUser = (id, data) => axios.put(`/users/${id}`, data);
export const apiDeactivateUser = (id) => axios.post(`/users/${id}/deactivate`);