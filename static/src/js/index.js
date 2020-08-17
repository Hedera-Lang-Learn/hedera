import '../scss/index.scss';

import Clipboard from 'clipboard';

import loadApps from './app';
import handleMessageDismiss from './messages';

import 'bootstrap/js/dist/util';
import 'bootstrap/js/dist/tab';
import 'bootstrap/js/dist/collapse';

loadApps();
handleMessageDismiss();

// eslint-disable-next-line no-new
new Clipboard('.btn-copy');
