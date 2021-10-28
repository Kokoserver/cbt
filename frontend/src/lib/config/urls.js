import {
	userBaseUrl,
	ExamBaseUrl,
} from '../config/request';

export const userEndpoint = {
	update: `${userBaseUrl}/update`,
	login: `${userBaseUrl}/login`,
	register: `${userBaseUrl}/create`,
	allUser: `${userBaseUrl}/alluser`,
	passwordLink: `${userBaseUrl}/password/reset/link`,
	resetPassword: `${userBaseUrl}/password/reset`,
	remove: `${userBaseUrl}/remove`
};
export const examEndpoint = {
	exam: `${ExamBaseUrl}`,
	login: `${ExamBaseUrl}/login`,
	score: `${ExamBaseUrl}/addscore`,
	create:`${ExamBaseUrl}/create`
};

