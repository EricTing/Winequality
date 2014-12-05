%% load data

winedata = load('winequality-red.dat');
[Y,I] = sort(winedata(:,end));
winedataSorted = winedata(I,:);

headers = {'fixed acidity';'volatile acidity';'citric acid';'residual sugar';'chlorides';'free sulfur dioxide';'total sulfur dioxide';'density';'pH';'sulphates';'alcohol';'quality'};
%% plot series data
figure(1)
hold on
for i = 1:(length(headers))
    subplot(6,2,i)
    hist(winedataSorted(:,i), 30);
    % plot(winedataSorted(:,i), 'b-'); % original
    % plot(winedataSorted_Discrete(:,i)); % discretized
    axis tight
    set(gca,'xtick',[])
    set(gca,'xticklabel',[])
    title(headers{i})
    Beautify(gca, 0)
end
hold off

%% calculate table of correlations
correlations = zeros(length(headers),length(headers));
for i = 1:(length(headers)-1)
    for j = (i):length(headers)
        c = corr(winedataSorted_Discrete(:,i), winedataSorted_Discrete(:,j));
        % c = corr(winedataSorted(:,i), winedataSorted(:,j));
        correlations(i,j) = c;
        % disp(sprintf('%20s & %20s:\t\t %g',headers{i}, headers{j}, c))
    end
end

%% discretization
winedataSorted_Discrete = zeros(size(winedata));
for i = 1:(length(headers)-1)
    d = winedataSorted(:,i);
	d_Discrete = ones(size(d));
    disp( sprintf('%s & %s: %8.5g; %8.5g','Max', 'Min', max(d), min(d)) )
    divisions = linspace(min(d), max(d), 5);
    d_Discrete(d>divisions(2)) = 2;
    d_Discrete(d>divisions(3)) = 3;
    d_Discrete(d>divisions(4)) = 4;
    winedataSorted_Discrete(:,i) = d_Discrete;
end
winedataSorted_Discrete(:,end) = winedataSorted(:,end);

%% write discretized data
dlmwrite('winequality-red-discrete.dat',winedataSorted_Discrete, 'delimiter', ',')

%% compare prediction and reality
predictedQuality = load('prediction.dat');
realQuality = winedataSorted(:,end);
figure(1)
hold on
plot(predictedQuality,'r')
plot(realQuality,'b')
hold off
sum((predictedQuality - realQuality)==0) % accuracy