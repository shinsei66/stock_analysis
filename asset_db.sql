-- なぜかUNIONにするとsyntaxエラーになる・・・
INSERT INTO asset_hist_stack (
    SELECT DATE_FORMAT(date,"%Y/%m/%d") as 'date'
    ,"cash" as 'dimension' 
    ,cash as 'value'
    , ym 
    from asset_hist
    ); 
INSERT INTO asset_hist_stack (
    SELECT DATE_FORMAT(date,"%Y/%m/%d") as 'date'
    ,"point" as 'dimension' 
    ,point as 'value'
    ,ym from asset_hist 
    ); 
INSERT INTO asset_hist_stack (
     SELECT DATE_FORMAT(date,"%Y/%m/%d") as 'date'
    ,"pension" as 'dimension' 
    ,pension as 'value', ym from asset_hist
    ); 
INSERT INTO asset_hist_stack (
     SELECT DATE_FORMAT(date,"%Y/%m/%d") as 'date'
    ,"trust" as 'dimension' 
    ,trust as 'value'
    ,ym from asset_hist 
    ); 
INSERT INTO asset_hist_stack (
     SELECT DATE_FORMAT(date,"%Y/%m/%d") as 'date'
    ,"stock" as 'dimension'
    ,stock as 'value'
    ,ym from asset_hist 
    ); 
INSERT INTO asset_hist_stack (
     SELECT DATE_FORMAT(date,"%Y/%m/%d") as 'date'
    ,"margin" as 'dimension'
    ,margin as 'value'
    ,ym from asset_hist);