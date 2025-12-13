```javascript
(url) => {
        if (!url) {
            url = window.location.href
        }
        if (url.indexOf('?') === -1) {
            return {}
        }
        let params = url.split('?')[1];
        let results = {};
        params.split('&').map(v => {
            let [name, value] = v.split('=');
            value = value.replace('#', '');
            value = unescape(value);
            results[name] = value
        })
        return results
    }
```