import { faArrowRight } from '@fortawesome/free-solid-svg-icons/faArrowRight';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons/faArrowLeft';
import { faCircle } from '@fortawesome/free-solid-svg-icons/faCircle';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons/faCaretDown';
import { faTimes } from '@fortawesome/free-solid-svg-icons/faTimes';
import { faDownload } from '@fortawesome/free-solid-svg-icons/faDownload';
import { faTrash } from '@fortawesome/free-solid-svg-icons/faTrash';
import { faPenFancy } from '@fortawesome/free-solid-svg-icons/faPenFancy';
import { faBan } from '@fortawesome/free-solid-svg-icons/faBan';
import { faCheck } from '@fortawesome/free-solid-svg-icons/faCheck';

const iconMap = [
  faArrowRight,
  faArrowLeft,
  faCircle,
  faCaretDown,
  faDownload,
  faTimes,
  faTrash,
  faPenFancy,
  faBan,
  faCheck,
].reduce((map, obj) => {
  map[obj.iconName] = obj;
  return map;
}, {});

export default iconMap;
