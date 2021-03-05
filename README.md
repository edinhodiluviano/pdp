# pdp
Programador desempregado e preguiçoso

# Formato de saída dos dados

```
{
    "raw": {
        "url": "https://some.domain.com/some/path",
    },
    "timestamp": "2021-03-05T05:14:30.301258",
    "hash": "0123456789ABCDEF",
    "spider": "some spider name",
    "version": "0123456789ABCDEF",
    "crawl": "2021-03-05T05:14:30.301258",
}
```

raw: o conteúdo do item, um dicionário, conforme enviado pela spider  
    url: todos os items já devem vir com uma chave "url"  
timestamp: o horário que o item foi coletado  
hash: o sha256 do json do conteúdo do item  
spider: o nome da spider  
version: o commit que no qual o código esta sendo executado  
crawl: o horário que o crawl foi iniciado
